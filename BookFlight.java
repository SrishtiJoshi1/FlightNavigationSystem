package airlinemanagementsystem;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.sql.*;
import com.toedter.calendar.JDateChooser;                                                                                                                               
import java.util.*;

public class BookFlight extends JFrame implements ActionListener {

    JTextField tfaadhar;
    JLabel tfname, tfnationality, tfaddress, labelgender, labelfname, labelfcode, pnrLabel;
    JButton bookflight, fetchButton, flight;
    Choice source, destination;
    JDateChooser dcdate;

    public BookFlight() {
        getContentPane().setBackground(Color.WHITE);
        setLayout(null);

        JLabel heading = new JLabel("Book Flight");
        heading.setBounds(420, 10, 500, 35);
        heading.setFont(new Font("Tahoma", Font.PLAIN, 32));
        heading.setForeground(Color.BLUE);
        add(heading);

        int labelX = 60;
        int fieldX = 220;
        int btnX = 380;
        int y = 60;
        int gap = 40;  // Vertical gap between components reduced

        JLabel lblaadhar = new JLabel("Aadhar");
        lblaadhar.setBounds(labelX, y, 150, 25);
        lblaadhar.setFont(new Font("Tahoma", Font.PLAIN, 16));
        add(lblaadhar);

        tfaadhar = new JTextField();
        tfaadhar.setBounds(fieldX, y, 150, 25);
        add(tfaadhar);

        fetchButton = new JButton("Fetch User");
        fetchButton.setBackground(Color.BLACK);
        fetchButton.setForeground(Color.WHITE);
        fetchButton.setBounds(btnX, y, 120, 25);
        fetchButton.addActionListener(this);
        add(fetchButton);

        y += gap;
        JLabel lblname = new JLabel("Name");
        lblname.setBounds(labelX, y, 150, 25);
        lblname.setFont(new Font("Tahoma", Font.PLAIN, 16));
        add(lblname);

        tfname = new JLabel();
        tfname.setBounds(fieldX, y, 150, 25);
        add(tfname);

        y += gap;
        JLabel lblnationality = new JLabel("Nationality");
        lblnationality.setBounds(labelX, y, 150, 25);
        lblnationality.setFont(new Font("Tahoma", Font.PLAIN, 16));
        add(lblnationality);

        tfnationality = new JLabel();
        tfnationality.setBounds(fieldX, y, 150, 25);
        add(tfnationality);

        y += gap;
        JLabel lbladdress = new JLabel("Address");
        lbladdress.setBounds(labelX, y, 150, 25);
        lbladdress.setFont(new Font("Tahoma", Font.PLAIN, 16));
        add(lbladdress);

        tfaddress = new JLabel();
        tfaddress.setBounds(fieldX, y, 150, 25);
        add(tfaddress);

        y += gap;
        JLabel lblgender = new JLabel("Gender");
        lblgender.setBounds(labelX, y, 150, 25);
        lblgender.setFont(new Font("Tahoma", Font.PLAIN, 16));
        add(lblgender);

        labelgender = new JLabel();
        labelgender.setBounds(fieldX, y, 150, 25);
        add(labelgender);

        y += gap;
        JLabel lblsource = new JLabel("Source");
        lblsource.setBounds(labelX, y, 150, 25);
        lblsource.setFont(new Font("Tahoma", Font.PLAIN, 16));
        add(lblsource);

        source = new Choice();
        source.setBounds(fieldX, y, 150, 25);
        add(source);

        y += gap;
        JLabel lbldest = new JLabel("Destination");
        lbldest.setBounds(labelX, y, 150, 25);
        lbldest.setFont(new Font("Tahoma", Font.PLAIN, 16));
        add(lbldest);

        destination = new Choice();
        destination.setBounds(fieldX, y, 150, 25);
        add(destination);

        try {
            Conn c = new Conn();
            String query = "select * from flight";
            ResultSet rs = c.s.executeQuery(query);

            Set<String> sources = new HashSet<>();
            Set<String> destinations = new HashSet<>();

            while (rs.next()) {
                String src = rs.getString("source");
                if (!sources.contains(src)) {
                    source.add(src);
                    sources.add(src);
                }

                String dest = rs.getString("destination");
                if (!destinations.contains(dest)) {
                    destination.add(dest);
                    destinations.add(dest);
                }
            }

        } catch (Exception e) {
            e.printStackTrace();
        }

        flight = new JButton("Fetch Flights");
        flight.setBackground(Color.BLACK);
        flight.setForeground(Color.WHITE);
        flight.setBounds(btnX, y, 120, 25);
        flight.addActionListener(this);
        add(flight);

        y += gap;
        JLabel lblfname = new JLabel("Flight Name");
        lblfname.setBounds(labelX, y, 150, 25);
        lblfname.setFont(new Font("Tahoma", Font.PLAIN, 16));
        add(lblfname);

        labelfname = new JLabel();
        labelfname.setBounds(fieldX, y, 150, 25);
        add(labelfname);

        y += gap;
        JLabel lblfcode = new JLabel("Flight Code");
        lblfcode.setBounds(labelX, y, 150, 25);
        lblfcode.setFont(new Font("Tahoma", Font.PLAIN, 16));
        add(lblfcode);

        labelfcode = new JLabel();
        labelfcode.setBounds(fieldX, y, 150, 25);
        add(labelfcode);

        y += gap;
        JLabel lbldate = new JLabel("Date of Travel");
        lbldate.setBounds(labelX, y, 150, 25);
        lbldate.setFont(new Font("Tahoma", Font.PLAIN, 16));
        add(lbldate);

        dcdate = new JDateChooser();
        dcdate.setBounds(fieldX, y, 150, 25);
        add(dcdate);

        y += gap + 10;
        bookflight = new JButton("Book Flight");
        bookflight.setBackground(Color.BLACK);
        bookflight.setForeground(Color.WHITE);
        bookflight.setBounds(fieldX, y, 150, 25);
        bookflight.addActionListener(this);
        add(bookflight);

        y += gap - 10;
        JLabel lblpnr = new JLabel("PNR Number");
        lblpnr.setBounds(labelX, y, 150, 25);
        lblpnr.setFont(new Font("Tahoma", Font.PLAIN, 16));
        add(lblpnr);

        pnrLabel = new JLabel();
        pnrLabel.setBounds(fieldX, y, 250, 25);
        pnrLabel.setFont(new Font("Tahoma", Font.BOLD, 16));
        pnrLabel.setForeground(Color.RED);
        add(pnrLabel);

        ImageIcon i1 = new ImageIcon(ClassLoader.getSystemResource("airlinemanagementsystem/icons/details.jpg"));
        Image i2 = i1.getImage().getScaledInstance(450, 320, Image.SCALE_DEFAULT);
        ImageIcon image = new ImageIcon(i2);
        JLabel lblimage = new JLabel(image);
        lblimage.setBounds(550, 80, 500, 410);
        add(lblimage);

        setSize(1100, 700);
        setLocation(200, 50);
        setVisible(true);
    }

    public void actionPerformed(ActionEvent ae) {
        if (ae.getSource() == fetchButton) {
            String aadhar = tfaadhar.getText();

            try {
                Conn conn = new Conn();
                String query = "select * from passenger where aadhar = '" + aadhar + "'";
                ResultSet rs = conn.s.executeQuery(query);

                if (rs.next()) {
                    tfname.setText(rs.getString("name"));
                    tfnationality.setText(rs.getString("nationality"));
                    tfaddress.setText(rs.getString("address"));
                    labelgender.setText(rs.getString("gender"));
                } else {
                    JOptionPane.showMessageDialog(null, "Please enter correct aadhar");
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        } else if (ae.getSource() == flight) {
            String src = source.getSelectedItem();
            String dest = destination.getSelectedItem();
            try {
                Conn conn = new Conn();
                String query = "select * from flight where source = '" + src + "' and destination = '" + dest + "'";
                ResultSet rs = conn.s.executeQuery(query);

                if (rs.next()) {
                    labelfname.setText(rs.getString("f_name"));
                    labelfcode.setText(rs.getString("f_code"));
                } else {
                    JOptionPane.showMessageDialog(null, "No Flights Found");
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        } else if (ae.getSource() == bookflight) {
            Random random = new Random();

            String aadhar = tfaadhar.getText();
            String name = tfname.getText();
            String nationality = tfnationality.getText();
            String flightname = labelfname.getText();
            String flightcode = labelfcode.getText();
            String src = source.getSelectedItem();
            String des = destination.getSelectedItem();
            String ddate = ((JTextField) dcdate.getDateEditor().getUiComponent()).getText();

            String pnr = "PNR-" + random.nextInt(1000000);
            String ticket = "TIC-" + random.nextInt(10000);

            try {
                Conn conn = new Conn();

                String query = "insert into reservation values('" + pnr + "', '" + ticket + "', '" + aadhar + "', '" + name + "', '" + nationality + "', '" + flightname + "', '" + flightcode + "', '" + src + "', '" + des + "', '" + ddate + "')";
                conn.s.executeUpdate(query);

                JOptionPane.showMessageDialog(null, "Ticket Booked Successfully\nPNR: " + pnr);
                pnrLabel.setText(pnr);

            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public static void main(String[] args) {
        new BookFlight();
    }
}
